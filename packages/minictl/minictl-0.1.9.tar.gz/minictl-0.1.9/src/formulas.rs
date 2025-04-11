// There is a lot of duplicated code here,
// across LTL and CTL, as they are somewhat similar.
//
// The amount of mess you have to create to make a generic parser
// with multiple modes is not worth it imo, so I just copy-pased and modified the code.
//
// This allows CTL and LTL to live completely seperate lives, which makes sense,
// as they are completely distinct logics.
use std::hash::Hash;

mod ctl_parse;
mod ctl_types;
pub use ctl_parse::{parse_ctl, CTLParseError};
pub(crate) use ctl_types::ctl_formula_macros;
pub use ctl_types::{memoize_ctl, CTLFactory, CTLFormula, CTLVariable};

mod ltl_parse;
mod ltl_types;
pub use ltl_parse::{parse_ltl, LTLParseError};
pub use ltl_types::{memoize_ltl, LTLFactory, LTLFormula, LTLVariable};

pub trait MLVariable: Eq + Hash {}

#[cfg(feature = "python")]
pub mod ctl_python;

#[cfg(feature = "python")]
pub mod ltl_python;
